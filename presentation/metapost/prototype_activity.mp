input metauml;

iActivity.foreColor := (1,1,1);

beginfig(1);
  Begin.b;
  Activity.download("Download needed data");
  Branch.missing_args;
  Activity.parse("Prepare data for output");
  Branch.missing_data;
  Activity.output_data("Append data to", "output stream");
  Activity.output_none("Append nothing to", "output stream");
  End.e;

  leftToRight(30)(b, missing_args);
  leftToRight.top(10)(output_data, output_none);
  Group.output(output_data, output_none);

  topToBottom(20)(missing_args, download, parse, missing_data, output, e);

  drawObjects(b, download, missing_args, missing_data, parse, output, e);

  clink(transition)(b, missing_args);
  clink(transition)(missing_args, download);
  clink(transition)(download, parse);
  clink(transition)(parse, missing_data);

  link(transition)(pathStepY(output_data.s, e.n, -10));
  link(transition)(pathStepY(output_none.s, e.n, -10));

  link(transition)(pathStepX(missing_args.e, e.e, 100));

  link(transition)(pathStepX(missing_data.w, output_data.n, -50));
  link(transition)(pathStepX(missing_data.e, output_none.n, 43.5));

  item(iGuard)("Needed arguments not given")(obj.sw = missing_args.s + (6, 6));
  item(iGuard)("All needed arguments given")(obj.ne = missing_args.s + (0, -1));

  item(iGuard)("No data found")(obj.sw = missing_data.s + (6, 6));
  item(iGuard)("Data found")(obj.se = missing_data.s + (-6, 6));
endfig;

end
